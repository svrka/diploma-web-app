// ? Do I need to use jQuery
var exam_id = '';
var chat = false;

function set_message_count(n) {
    $('#message_count').text(n);
    $('#message_count').css('visibility', n ? 'visible' : 'hidden');
}

function add_new_messages(m) {
    var msg = $("<p></p>").text(m);
    $('#new_messages').prepend(msg);
}

$(function () {
    var since = 0;
    if ($('#new_messages').length) {
        chat = true;
        exam_id = $(location).attr('pathname').split('/')[2];
    };
    // TODO: Decrease interval
    setInterval(function () {
        $.ajax('/messages?s=' + since + '&c=' + chat + '&e=' + exam_id).done(
            function (messages) {
                for (var i = 0; i < messages.length; i++) {
                    if (messages[i].status) {
                        if (($('#new_messages').length) && (messages[i].exam_id == parseInt(exam_id))) {
                            var message = messages[i].author + ': ' + messages[i].body;
                            // TODO: Flag new messages
                            add_new_messages(message);
                        } else set_message_count(messages[i].payload_json);
                        // ? Almost always 0
                        since = messages[i].timestamp;
                    };
                };
            }
        );
    }, 10000);
});

$(function () {
    $('#message_form').on('submit', function (e) {

        $.ajax({

            data: {
                message: $('#message').val(),
                exam_id: exam_id
            },
            type: 'POST',
            url: '/send_message'

        }).done(function (data) {

            $('#message').val('');
            var msg = data.author + ': ' + data.message;
            add_new_messages(msg);

        });

        e.preventDefault();
    });

    $('#message_form').keypress((e) => {

        if (e.which === 13) {
            $('#message_form').submit();
        }

    });
});


