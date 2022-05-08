import Widget from 'rasa-webchat';
const WebChatWidget = () => {
  return (
    <Widget
      socketUrl={'http://localhost:5005'}
      socketPath={'/socket.io/'}
      initPayload={'/greet'}
      title={'Brainy'}
      subtitle={'Your Virtual Assistant'}
      embedded={false}
      showMessageDate={true}
    />
  );
};
export default WebChatWidget;
