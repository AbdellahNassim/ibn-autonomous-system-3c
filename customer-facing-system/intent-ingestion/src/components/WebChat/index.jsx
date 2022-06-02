import Widget from 'rasa-webchat';
import '../../index.css';
import BrainyPdP from '../../assets/BrainyPdp.png';
import StartIcon from '../../assets/shuttle.png';
const WebChatWidget = () => {
  console.log(process.env['REACT_APP_INTENT_RECOGNITION_HOST']);
  return (
    <div id="widget">
      <Widget
        socketUrl={`http://${process.env['REACT_APP_INTENT_RECOGNITION_HOST']?process.env['REACT_APP_INTENT_RECOGNITION_HOST'] :'localhost' }:5005`}
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
