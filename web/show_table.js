import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// Displays input text on a node
// console.log("Received text:", text); // 打印接收到的文本

// // 检查 text 是否是数组
// if (Array.isArray(text)) {
//   // 将字符数组重新组合成字符串
//   text = text.join('');
// }

// try {
//   console.log("Received JSON:", text);
//   // 第一次解析：将字符数组转换为字符串
//   let parsedData = JSON.parse(text);
//   console.log("parsedData:", parsedData);

function registerColorNode(nodeName) {
  app.registerExtension({
    name: `baikong.${nodeName}`,
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
      if (nodeData.name === nodeName) {
        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
    
        if (this.widgets) {
          const pos = this.widgets.findIndex((w) => w.name === "result");
          if (pos !== -1) {
          for (let i = pos; i < this.widgets.length; i++) {
            this.widgets[i].onRemove?.();
          }
          this.widgets.length = pos;
          }
        }
    
        const w = ComfyWidgets["STRING"](this, "result", ["STRING", { multiline: true }], app).widget;
        w.inputEl.readOnly = true;
        w.inputEl.style.opacity = 0.6;

        let text = message.text;
        if (Array.isArray(text)) {
          // 将字符数组重新组合成字符串
          text = text.join('');
        }

        try {
          console.log("Received JSON:", text);
          // 第一次解析：将字符数组转换为字符串
          let parsedData = JSON.parse(text);
          console.log("parsedData:", parsedData);

          w.value = JSON.stringify(parsedData, null, 2);
        } catch(error) {
          console.error("JSON 解析错误:", error);
        }
        
  
        this.onResize?.(this.size);
        };
      }
    },
  });
}

registerColorNode("BK_Table_Preview");