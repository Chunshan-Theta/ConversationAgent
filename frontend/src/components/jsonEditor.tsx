import React from 'react';
import logo from './logo.svg';
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-json";
import "ace-builds/src-noconflict/theme-monokai";
import {botSample} from "./sampleBot";
function onChange(newValue: string) {
  console.log("change", newValue);
}
type Editor = {
  editorId: string
}
function BotEditor(prop: Editor) {
  let divId: string = prop.editorId || "editor";
  return (
    <div>
    <AceEditor
        mode="json"
        theme="monokai"
        name={divId}
        onChange={onChange}
        editorProps={{ $blockScrolling: true }}
        setOptions={{
          useWorker: false
        }}
        value={JSON.stringify(botSample, null, 2)}
        
      />
    </div>
  );
  
}

function MemoryEditor(prop: Editor) {
  let divId: string = prop.editorId || "editor";
  return (
    <div>
    <AceEditor
        mode="json"
        theme="monokai"
        name={divId}
        onChange={onChange}
        editorProps={{ $blockScrolling: true }}
        setOptions={{
          useWorker: false
          
        }}
        value='{}'
        
      />
    </div>
  );
  
}

export {BotEditor, MemoryEditor};

