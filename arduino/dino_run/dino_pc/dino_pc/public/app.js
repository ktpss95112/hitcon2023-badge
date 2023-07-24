const wsProto = location.protocol === "http:" ? "ws:" : "wss:";
const wsUrl = `${wsProto}//${location.host}/ws`;

// https://stackoverflow.com/questions/22431751/websocket-how-to-automatically-reconnect-after-it-dies
function connect() {
  const ws = new WebSocket(wsUrl);
  // ws.onopen = function () {};

  ws.onmessage = function (e) {
    try {
      const data = JSON.parse(e.data);
      const { event } = data;
      if ("error" in data) {
        if (data.error === "window_opened") {
          alert("There is an opened game.\nPlease close the window.");
        }
      } else if (event === "card_down" || event === "card_up") {
        console.log(data);
        if (window.Runner !== undefined) {
          // Runner is singleton
          cardEventHandler(data, new window.Runner());
        }
      }
    } catch {
      // ignore
    }
  };

  ws.onclose = function (e) {
    console.log(
      "Socket is closed. Reconnect will be attempted in 1 second.",
      e.reason
    );
    setTimeout(function () {
      connect();
    }, 1000);
  };

  ws.onerror = function (err) {
    console.error("Socket encountered error: ", err.message, "Closing socket");
    ws.close();
  };
}

connect();

function cardEventHandler(data, runner) {
  const mockKeyEvent = {
    preventDefault() {},
    keyCode: 32,
    target: document.getElementById("t"),
  };
  const { event, uid } = data;
  if (event === "card_down") {
    runner.onKeyDown(mockKeyEvent);
    document.onkeydown(mockKeyEvent);
  } else if (event === "card_up") {
    runner.onKeyUp(mockKeyEvent);
    document.onkeydown(mockKeyEvent);
  }
}
