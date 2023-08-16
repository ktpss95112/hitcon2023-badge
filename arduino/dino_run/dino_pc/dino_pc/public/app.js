const wsProto = location.protocol === "http:" ? "ws:" : "wss:";
const wsUrl = `${wsProto}//${location.host}/ws`;

// https://stackoverflow.com/questions/22431751/websocket-how-to-automatically-reconnect-after-it-dies
function connect() {
  const ws = new WebSocket(wsUrl);
  // ws.onopen = () => { };

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

function setCardUid(uid) {
  if (window.cardUid !== undefined && window.cardUid !== uid) {
    location.reload();
  } else {
    window.cardUid = uid;
  }
}

let cardState = "up";

function cardEventHandler(data, runner) {
  const mockKeyEvent = {
    preventDefault() {},
    keyCode: 32,
    target: document.getElementById("t"),
  };
  const { event, uid } = data;
  if (event === "card_down" && uid.length === 8) {
    cardState = "down";
    runner.onKeyDown(mockKeyEvent);
    document.onkeydown(mockKeyEvent);
    setCardUid(uid);
  } else if (event === "card_up" && uid.length === 8) {
    if (cardState === "down") {
      cardState = "up";
      runner.onKeyUp(mockKeyEvent);
      document.onkeydown(mockKeyEvent);
      setCardUid(uid);
    }
  }
}

function gameOver(distanceRan) {
  const score = Math.ceil(distanceRan);
  // the api get score from query now, is that a bug?
  if (window.cardUid) {
    fetch(`/proxy/dinorun/${window.cardUid}?score=${score}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ score }),
    }).then(async (resp) => {
      const Toast = Swal.mixin({
        toast: true,
        position: "bottom-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      if (resp.status < 200 || resp.status >= 300) {
        const text = await resp.text();
        Toast.fire({
          icon: "error",
          title: "Score uploading failed 😵",
          text: `[${resp.status}] ${text}`,
        });
      } else {
        Toast.fire({
          icon: "success",
          title: "Score uploaded 🏆",
        });
      }
    });
  }
}
