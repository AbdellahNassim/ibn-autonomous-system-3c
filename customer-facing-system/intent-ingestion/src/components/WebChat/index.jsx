import Widget from 'rasa-webchat';
import '../../index.css';
import BrainyPdP from '../../assets/BrainyPdp.png';
const WebChatWidget = () => {
  return (
    <div id="widget">
      <Widget
        socketUrl={'http://localhost:5005'}
        socketPath={'/socket.io/'}
        initPayload={'/greet'}
        title={'Brainy'}
        subtitle={'Your Virtual Assistant'}
        embedded={false}
        profileAvatar={BrainyPdP}
        showMessageDate={true}
      />
    </div>
  );
};
export default WebChatWidget;
