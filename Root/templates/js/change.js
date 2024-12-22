  // Socket.IOの接続を確立
  const socket = io();

  // 'navigate' イベントを受け取ったらページ遷移を実行
  socket.on('navigate', function(data) {
    if (data.url) {
      console.log('Navigating to:', data.url);
      window.location.href = data.url;
    } else {
      console.error('No URL provided for navigation.');
    }
  });