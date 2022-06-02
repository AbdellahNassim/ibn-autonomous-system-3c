import Widget from 'rasa-webchat';
import '../../index.css';
import BrainyPdP from '../../assets/BrainyPdp.png';
import StartIcon from '../../assets/shuttle.png';
const WebChatWidget = () => {
  return (
    <div id="widget">
      <Widget
        socketUrl={`http://${process.env['INTENT_RECOGNITION_HOST']?process.env['INTENT_RECOGNITION_HOST'] :'localhost' }:5005`}
        socketPath={'/socket.io/'}
        initPayload={'/greet'}
        title={'Brainy'}
        subtitle={'Your Virtual Assistant'}
        embedded={false}
        profileAvatar={BrainyPdP}
        showMessageDate={true}
        openLauncherImage={StartIcon}
        inputTextFieldHint={'I want a video service '}
      />
    </div>
  );
};
export default WebChatWidget;
