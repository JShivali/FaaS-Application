import './App.css';
import React, { Component } from 'react'
import Form from './components/Form';
import {BounceLoader} from 'react-spinners'

class App extends Component {
  render(){
    return(
      <div className="App">
        <Form />
      </div>
    )
  }
}

export default App;
