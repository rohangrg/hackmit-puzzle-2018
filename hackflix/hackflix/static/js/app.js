$(function() {
  var video = document.querySelector('.player-vid');

  function checkLoad() {
      if (video.readyState === 4) {
          $('.ui.dimmer').removeClass('active');
      } else {
          setTimeout(checkLoad, 100);
      }
  }

  function fetchUpdates() {
    $.get(VIDEO_INFO_URL, function(data) {
      if(data.rendered) {
        console.log('hi');
        video.src = data.url;
        video.load();
        checkLoad();
      } else {
        setTimeout(fetchUpdates, 2000);
      }
    });
  }

  fetchUpdates();
});
