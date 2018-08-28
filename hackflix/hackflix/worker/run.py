from hackflix.worker.models import Session, GenerateVideoRequest, VerifySolutionRequest
from datetime import datetime, timedelta
import time
import tempfile
import os
import sys

from hackflix.puzzle.encoder import process_video, FPS, FRAMES
from hackflix.utils import username_to_mp4, username_pick_range
from hackflix.puzzle.decoder import attempt_decode
from hackflix.config import DURATION

def process_generate_video_request(generate_request):
    filename, original_name, _, _ = username_to_mp4(generate_request.username)
    tf, tfo = tempfile.mkstemp(suffix='.mp4'), tempfile.mkstemp(suffix='.mp4')

    duration = int(FPS * DURATION)
    start = username_pick_range(generate_request.username, FRAMES - duration)
    process_video(tf[1], tfo[1], generate_request.username, start, start + duration)

    os.fchmod(tfo[0], 0o700)
    os.close(tfo[0])
    os.rename(tfo[1], original_name)
    os.fchmod(tf[0], 0o755)
    os.close(tf[0])
    os.rename(tf[1], filename)

def process_verify_solution_request(verify_request):
    _, original_name, _, _ = username_to_mp4(verify_request.username)
    result = attempt_decode(original_name,
                            verify_request.upload_filename,
                            verify_request.username,
                            seed=username_pick_range(verify_request.username, 10000))

    return result

def run_worker():
    print("STARTING WORKER")
    sys.stdout.flush()
    session = Session()
    while True:
        session.query(GenerateVideoRequest).filter(GenerateVideoRequest.claimed_at <= datetime.now() - timedelta(minutes=2), GenerateVideoRequest.completed_at==None).delete()
        session.commit()

        generate_request = session.query(GenerateVideoRequest).filter(GenerateVideoRequest.claimed_at==None).with_for_update().first()
        if generate_request != None:
            print("GOT GENERATE REQUEST", generate_request)
            sys.stdout.flush()
            generate_request.claimed_at = datetime.now()
            session.commit()
            
            process_generate_video_request(generate_request)

            generate_request.completed_at = datetime.now()
            session.commit()
        
        verify_request = session.query(VerifySolutionRequest).filter(VerifySolutionRequest.claimed_at==None).with_for_update().first()
        if verify_request != None:
            print("GOT VERIFY REQUEST", verify_request)
            sys.stdout.flush()
            verify_request.claimed_at = datetime.now()
            session.commit()
            
            verify_request.result = process_verify_solution_request(verify_request)

            verify_request.completed_at = datetime.now()
            session.commit()

        time.sleep(0.1)
        sys.stdout.flush()
    session.close()

