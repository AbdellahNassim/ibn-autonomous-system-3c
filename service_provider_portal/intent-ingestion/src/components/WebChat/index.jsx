import React from 'react';
import Widget from 'rasa-webchat';
import '../../index.scss';
import BrainyPdP from '../../assets/BrainyPdp.png';
import StartIcon from '../../assets/shuttle.png';
import {useAuth} from '../../utils/auth';

const WebChatWidget = () => {
  const auth = useAuth();
  return (
    <div id="widget">
      <Widget
        socketUrl={`http://${process.env['REACT_APP_INTENT_RECOGNITION_HOST']?process.env['REACT_APP_INTENT_RECOGNITION_HOST'] :'localhost' }:5005`}
        socketPath={'/socket.io/'}
        initPayload={'/greet'}
        title={'Brainy'}
        autoClearCache={true}
        subtitle={'Your Virtual Assistant'}
        embedded={false}
        customData={{user: auth.getCurrentUser()}}
        profileAvatar={BrainyPdP}
        showMessageDate={true}
        openLauncherImage={StartIcon}
        inputTextFieldHint={'I want a video service '}
      />
    </div>
  );
};
export default WebChatWidget;
