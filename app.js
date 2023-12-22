import firebase from 'firebase/app'
import 'firebase/storage'
import {upload} from './upload.js'

const firebaseConfig = {
  apiKey: "AIzaSyBH_-OpMPZPLp_i0m7nPsLyyIv5N_rLUyE",
  authDomain: "object-vision-b854b.firebaseapp.com",
  projectId: "object-vision-b854b",
  storageBucket: "object-vision-b854b.appspot.com",
  messagingSenderId: "903595349702",
  appId: "1:903595349702:web:f4f733e08ce150fcdb29c7"
};

firebase.initializeApp(firebaseConfig)

const storage = firebase.storage()

// const pyFunc = async(url) => {
//   await loadPyodide({ indexURL : "https://cdn.jsdelivr.net/pyodide/v0.17.0/full/" });
//   const module = await pyodide.loadPackage(['numpy']);
//   const result = await module.runPythonAsync('import numpy\nnumpy.random.rand()');
// }

upload('#file', {
  multi: true,
  accept: ['.png', '.jpg', '.jpeg', '.gif'],
  onUpload(files, blocks) {
    files.forEach((file, index) => {
      const ref = storage.ref(`images/${file.name}`)
      const task = ref.put(file)

      task.on('state_changed', snapshot => {
        const percentage = ((snapshot.bytesTransferred / snapshot.totalBytes) * 100).toFixed(0) + '%'
        const block = blocks[index].querySelector('.preview-info-progress')
        block.textContent = percentage
        block.style.width = percentage
      }, error => {
        console.log(error)
      }, () => {
        task.snapshot.ref.getDownloadURL().then(url => {
          console.log('Download URL', url)
        })
      })
    })
  }
})