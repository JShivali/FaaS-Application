import React, { Component } from 'react';
import {BeatLoader} from 'react-spinners';
import {Button,Select, MenuItem, FormControl, InputLabel, TextField,FormLabel, Input} from '@material-ui/core';
import {ThemeProvider} from '@material-ui/core/styles';
import theme from '../theme';
import {css} from '@emotion/react';



const loaderCSS= css`    
        margin-top:25px;
        margin-bottom:25px;
        justify-content: "center";
        align-items: "center";
        position: "relative";
      `




 class Form extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
            bookurl:'' ,
            imageurl:'',
            showImage:false,
            loading:false
        }
    }

    handlerBookUrlChange=(event)=>{
        this.setState({
            bookurl:event.target.value
        })
    }

    handleSelectBookUrl=(event)=>{
        this.setState({
            bookurl:event.target.value
        })
    }

    handleSubmit= event =>{
        event.preventDefault();
        
        
        this.setState({
            showImage:false,
            loading:true
        })
        this.setState({
            imageurl:''
        })
        const response=getSummary(this.state.bookurl)
        response.then(result=>this.setState({
            showImage:true,
            imageurl:result,
            loading:false
        }))
        response.then(result=>console.log(result))
        
    }

    showImage = () => {
        return (
         
                <img src={this.state.imageurl} alt="" />
          );
      }

    
    

    render() {
        
        return (
            <ThemeProvider theme={theme}>
                <div id="page">
            <form onSubmit={this.handleSubmit}>
                
                <div id="header">
                <h1>Enter a book url or select from the dropdown</h1>
                </div>
                
            <div id="urltextbox">
                    <TextField type="text" value={this.state.bookurl} onChange={this.handlerBookUrlChange} placeholder="paste the url of the book"></TextField>
                </div>
                <div id="inputarea">
                    <FormControl id="formcontrol">
                    
                    <Select value={this.state.topic} onChange={this.handleSelectBookUrl} autoWidth={false} defaultValue="def">
                    <MenuItem value="def">select a book</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/1342/1342-0.txt">Pride and Prejudice</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/91/91-0.txt">Tom Sawyer Abroad</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/1524/1524-0.txt">Hamlet</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/98/98-8.txt">A Tale of Two Cities</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/11/11-0.txt">Alice in the Wonderland</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/1661/1661-0.txt">Adventures of Sherlock Holmes</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/236/236-0.txt">The Jungle book</MenuItem>
                        <MenuItem value="http://www.gutenberg.org/files/57/57.txt">Aladdin and the Magic Lamp</MenuItem>
                    </Select>
                    
                    </FormControl>
                </div>
                <div id="btndiv">
                <Button type="submit" variant="contained" color="primary"> Get statistics </Button>
                </div>
                <div id="beatloader">
                <BeatLoader  loading={this.state.loading}  />
                </div>
                <div id="outputdiv">
                {this.state.showImage? this.showImage() : null}
                </div>
                
            </form>
            </div>
         
                
            </ThemeProvider>
        )
    }
}

async function getSummary(bookurl){
    const msg=JSON.stringify(
        {
        message:bookurl
    });
    console.log(msg);
    const proxyurl = "https://cors-anywhere.herokuapp.com/";
    const url = "https://us-central1-cloud-map-reduce.cloudfunctions.net/fetch-data"; 
    const requestOptions={
        
            method:'POST',
            body: msg,
            headers:{
                'Accept': 'application/json',
                'Content-Type':'application/json',
            }
            
    };
    const response=await fetch(proxyurl+url,requestOptions).then(res=>res.text())
    
    return response
    
    
}

export default Form;
