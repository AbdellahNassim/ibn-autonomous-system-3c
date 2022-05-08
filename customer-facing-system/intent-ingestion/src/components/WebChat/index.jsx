import Widget from 'rasa-webchat';

const WebChatWidget = () => {
  return (
    <Widget
      socketUrl={'http://localhost:5005'}
      socketPath={'/socket.io/'}
      initPayload={'/greet'}
      customData={{'language': 'en'}} // arbitrary custom data. Stay minimal as this will be added to the socket
      title={'Brainy'}
    />
  );
};
export default WebChatWidget;
