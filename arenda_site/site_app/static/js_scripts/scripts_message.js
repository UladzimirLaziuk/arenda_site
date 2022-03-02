const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/bot/'
    );

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    var NoResultsLabel = "No Results";
    var availableTags = ''
    if (data.index != null) {
        var availableTags = [
                         (data.message),
                         ];
    }

    function triggerAutoComplete() {
    $("#chat-message-input").autocomplete({
        position: {
                my: "left bottom",
                at: "left top",
                collision: "flip flip"
            },
        source: function(request, response) {
            var results = $.ui.autocomplete.filter(availableTags, request.term.split("#")[1]);
            if (!results.length) {
                results = [NoResultsLabel];
            }
            response(results);
        },
        select: function (event, ui) {
            if (ui.item.label === NoResultsLabel) {

                event.preventDefault();
            }
        },
    });
}


    triggerAutoComplete();
    $("#chat-message-input").trigger('keydown');
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');

    const message = messageInputDom.value.split("#")[1];
    chatSocket.send(JSON.stringify({
        'message': message
    }));
};


