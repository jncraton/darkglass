;(() => {
  const markedScript = document.createElement('script')
  markedScript.src = 'https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js'
  markedScript.defer = true
  document.head.appendChild(markedScript)

  const styles = `
    #darkglass {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 300px;
      height: 36px;
      max-width: 80vw;
      font-family: sans-serif;
      font-size: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      border: 1px solid #ccc;
      border-radius: 8px;
      overflow: hidden;
      z-index: 9999;
      transition: height 0.3s ease
    }
    #darkglass.closed {
      width: 200px
    }
    #darkglass .header {
      background: #8b2404;
      color: #fff;
      padding: 8px 10px;
      cursor: pointer;
      user-select: none
    }
    #darkglass .body {
      display: flex;
      flex-direction: column;
      height: 300px;
      background: #fff
    }
    #darkglass.closed .body {
      display: none
    }
    #darkglass .messages {
      flex: 1;
      padding: 10px;
      overflow: auto;
      background: #fafafa
    }
    #darkglass .input-container {
      border-top: 1px solid #ddd;
      padding: 5px
    }
    #darkglass .input-container input {
      width: 100%;
      box-sizing: border-box;
      padding: 6px;
      border: 1px solid #ccc;
      border-radius: 4px
    }
  `

  const style = document.createElement('style')
  style.textContent = styles
  document.head.appendChild(style)

  const base = (() => {
    let script = document.currentScript
    if (!script) {
      const scripts = document.getElementsByTagName('script')
      script = scripts[scripts.length - 1]
    }
    if (!script || !script.src) {
      return window.location.origin
    }
    return new URL(script.src, window.location).origin
  })()

  const iframe = document.createElement('iframe')
  iframe.id = 'darkglass'
  iframe.src = base + '/static/webchat.html'
  iframe.style.position = 'fixed'
  iframe.style.bottom = '20px'
  iframe.style.right = '20px'
  iframe.style.width = '300px'
  iframe.style.maxWidth = '80vw'
  iframe.style.height = '36px'
  iframe.style.border = '0'
  iframe.style.zIndex = '9999'
  iframe.style.transition = 'height 0.3s ease'

  window.addEventListener('message', (e) => {
    if (e.data && e.data.type === 'height') {
      iframe.style.height = e.data.height + 'px'
    }
  })
  document.body.appendChild(iframe)
})()
