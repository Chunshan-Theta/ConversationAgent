import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/row.css';
import './css/jsonEditor.css';
import {BotEditor, MemoryEditor} from './components/jsonEditor';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>

      <h1>Bot Data</h1>
        <div className="container">
          <div className="left-half">
            {/* <!-- 这里放右边区域的内容 --> */}
              <BotEditor editorId="e1"/>
              
          </div>
          <div className="right-half">
              {/* <!-- 这里放右边区域的内容 --> */}
              <MemoryEditor editorId="e2" />
          </div>
        </div>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
