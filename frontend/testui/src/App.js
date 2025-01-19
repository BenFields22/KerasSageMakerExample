import React from "react";
import "./App.css"

class App extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.getRate = this.getRate.bind(this);
    this.state = {
      ID:"None Loaded",
      BestRate: "None Loaded",
      AllRates: "None Loaded",
      Inference: "None Loaded",
      selection:1,
    }
  }

  async componentDidMount(){
    
  }

  UpdateSelection = (e) =>{
    //console.log(e.target.value);
    this.setState({selection: e.target.value});
  }

  async getRate(){
    const myid = this.state.selection;
    const response = await fetch("your-api-gateway-endpoint", {
      method: "POST", // Change to the desired method
      headers: {
        "Content-Type": "application/json", // Specify the content type
      },
      body: JSON.stringify({'id': `${myid}`}),
    });
    const data = await response.json();
    //console.log(data);
    //console.log(data.body.bestRate);
    this.setState({ID:data.body.id,BestRate:data.body.bestRate,AllRates:data.body.allrates,Inference:data.body.prediction});
  }

  render() {
    const options = Array.from({ length: 100 }, (_, index) => index + 1);
    return (
      <div className="Container">
        <br/>
        <div>
      <label htmlFor="numberSelector">Select a Hotel ID:</label>
      <select id="numberSelector" name="numberSelector" onChange={this.UpdateSelection}>
        {options.map((number) => (
          <option key={number} value={number}>
            {number}
          </option>
        ))}
      </select>
    </div> 
      <button onClick={this.getRate}>Get Top Rating</button>
      <div>ID: {JSON.stringify(this.state.ID, null,2)}</div> 
      <div>All Ratings: {JSON.stringify(this.state.AllRates, null, 2)}</div>
      <div>Inference: {JSON.stringify(this.state.Inference, null, 2)}</div>
      <div>Best Rating: {JSON.stringify(this.state.BestRate, null,2)}</div>
      
      </div>
    );
  }
};

export default App;