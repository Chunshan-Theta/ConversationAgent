import { useState, useEffect } from 'react';
import logo from './logo.svg';
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-json";
import "ace-builds/src-noconflict/theme-monokai";
import {botSample} from "./sampleBot";



type Editor = {
  editorId: string
}


function BotEditor(prop: Editor) {
  console.log();
  const [msgOfSystem, setMsgOfSystem] = useState("");
  const [valueOfBot, setValueOfBot] = useState("{}");

  let divId: string = prop.editorId || "editor";
  const initBot = () => {
    setValueOfBot(JSON.stringify(botSample, null, 2));
  };
  const changeFunc = (value: string) => setValueOfBot(value);
  const beautify = () => {
    try {
      
      const obj = JSON.parse(valueOfBot);
      setValueOfBot(JSON.stringify(obj, null, 2));
      setMsgOfSystem("");
      
    } catch ({name, message}) {
      setMsgOfSystem(name+": "+message);
    }
  
  };

  
  return (
    <div>
    <AceEditor
        mode="json"
        theme="monokai"
        name={divId}
        onChange={changeFunc}
        editorProps={{ $blockScrolling: true }}
        setOptions={{
          useWorker: false,
          enableAutoIndent: true,
          enableLiveAutocompletion: true
        }}
        value={valueOfBot}
        
      />
    <button onClick={initBot}>Init</button>

    <button onClick={beautify}>Beautify</button>
    <div >{msgOfSystem}</div>
    </div>
  );
  
}
function MemoryEditor(prop: Editor) {
  console.log();
  const [msgOfSystem, setMsgOfSystem] = useState("");
  const [valueOfMemory, setValueOfMemory] = useState("{}");

  let divId: string = prop.editorId || "editor";
  const initMemory = () => setValueOfMemory("{}");

  const changeFunc = (value: string) => setValueOfMemory(value);
  const beautify = () => {
    try {
      
      const obj = JSON.parse(valueOfMemory);
      setValueOfMemory(JSON.stringify(obj, null, 2));
      setMsgOfSystem("");
      
    } catch ({name, message}) {
      setMsgOfSystem(name+": "+message);
    }
  
  };

  
  return (
    <div>
    <AceEditor
        mode="json"
        theme="monokai"
        name={divId}
        onChange={changeFunc}
        editorProps={{ $blockScrolling: true }}
        setOptions={{
          useWorker: false,
          enableAutoIndent: true,
          enableLiveAutocompletion: true
        }}
        value={valueOfMemory}
        
      />
    <button onClick={initMemory}>Init</button>

    <button onClick={beautify}>Beautify</button>
    <div >{msgOfSystem}</div>
    </div>
  );
  
}


export {BotEditor, MemoryEditor};

