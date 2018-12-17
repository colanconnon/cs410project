import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { withRouter } from "react-router";
import * as qs from 'query-string';



const UploadSuccess = () => (
  <div className="container">
    <h3 className="mt-5 text-success">
    Upload successful, please wait for the file to be processed and indexed before
    appearing in search results. Depending on the size of the video this can take a while.
    </h3>
  </div>
)

const UploadVideoForm = () => ( 
      <div className="container">
        <h3 className="mt-5">
          Upload New Video
        </h3>
        <p className="text-muted">
        This uploaded video will be transcribed and summarized, then will appear in search results.
        </p>
      <form action="/api/upload-file/" method="POST" encType="multipart/form-data">
        <div className="form-group">
            <input className="form-control-file" name="file" type="file" />
            <p className="form-text text-muted">Only videos with mp4 format are permitted</p>
        </div>
        <input type="submit" value="submit" className="btn btn-primary" />
      </form>
     </div>
)


class SearchForm extends Component {

   constructor(props) {
     super(props);
     this.state = {
       query: ''
     }
   }
   onSubmit = (e) => {
     e.preventDefault();
     this.props.history.push(`/search-results?q=${this.state.query}`)
   }

  render() {
    return (

  <div className="container">
	<div className="row justify-content-center mt-5">
      <h3 className="mt-5">
        Search
      </h3>
  </div>
  <form onSubmit={this.onSubmit} >
  
	<div className="row justify-content-center">
   <input onChange={(e) => {this.setState({'query': e.target.value} ) } } type="text" className="fom-control form-control-lg mt-4 col-md-8" />
   </div>
  
	<div className="row justify-content-center mt-3">
   <button type="submit" className="btn btn-primary"> Search </button>
   </div>
  
  </form>
  </div>
    ) 
  }
}

class SearchResults extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: qs.parse(this.props.location.search).q,
      results: []
    }
  }
  async componentDidMount() {
      let result  = await fetch(`/api/search-engine/?q=${this.state.query}`)
      let json = await result.json();
      console.log(json);
      this.setState({
        results: json
      })
  }

  render() {
    return (
        <div className="container">
        <div className="row justify-content-center mt-3">
            <h3>
              Search Results for query: {this.state.query}
            </h3>
        </div>
        <div className="row">
        
          {this.state.results.map(result => {
              return(
                <div key={result.video_id} className="col-md-5 offset-md-1 mt-3">
                <div className="card" style={{width: "30rem"}}>
                <video currentTime={Number(result.start_match)} className="card-img-top" controls src={result.url}></video>
                <div className="card-body">
                <p className="text-muted">Start Time: {Number(result.start_match)} </p>
                <h5 className="card-title">Topics: {result.topics.join(", ")} </h5>
                <p className="card-text"> Summary: {result.summary} </p>
                </div>
                </div>
                </div>
              )

          })}
        </div>
      </div>
    )
  }
}

class App extends Component {
  render() {
    return (
      <div className="App">
       <Router>
       <div>
      <ul className="nav navbar-dark bg-dark">
        <li className="nav-item">
          <Link className="nav-link active" to="/">Search</Link>
        </li>
       <li className="nav-item">
         <Link className="nav-link" to='/upload-video'>Upload Video</Link>
       </li>
      </ul>
            <Route path="/" exact component={withRouter(SearchForm)} />
            <Route path="/search-results" component={SearchResults} />
            <Route path="/upload-video" component={UploadVideoForm} />
            <Route path="/success-upload" component={UploadSuccess} />
      </div>
      </Router>
      </div>
    );
  }
}

export default App;
