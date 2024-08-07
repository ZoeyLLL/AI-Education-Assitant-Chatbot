var $messages = $('.messages-content'),
    d, h, m;

$(window).load(function() {
  $messages.mCustomScrollbar();
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date();
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getUTCHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  var msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  sendMessageToServer(msg);
}

function sendMessageToServer(message) {
  fetch(`/query/${message}`)
    .then(response => response.json())
    .then(data => displayServerMessage(data))
    .catch(error => console.error('Error:', error));
}

function displayServerMessage(data) {
  var responseMessage = data.answer; // Assuming the server responds with an object containing an 'answer' key
  console.log(data);
  $('<div class="message new">' + responseMessage + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  updateScrollbar();
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
});
