using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PickController : MonoBehaviour {
    public GameObject pick;
    public Text error;

    float detectAngle;
	// Use this for initialization
	void Start () {
        detectAngle = Random.Range(-90f, 90f);
    }

    bool invoked = false;
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKey("left")) {
            pick.GetComponent<Rigidbody2D>().AddTorque(200.0f);
        } else if (Input.GetKey("right")) {
            pick.GetComponent<Rigidbody2D>().AddTorque(-200.0f);
        }

        float a = pick.transform.rotation.eulerAngles.z;

        if (a > 180) {
            a = - (360 - a);
        }

        error.text = string.Format("Error: {0}", a - detectAngle);

        if (Mathf.Abs(a - detectAngle) <= 5) {
            if (!invoked) {
                invoked = true;
            }
        } else {
            invoked = false;
            CancelInvoke("Unlock");
        }
	}
}
