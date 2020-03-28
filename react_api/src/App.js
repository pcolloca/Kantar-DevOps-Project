import React, {Component} from 'react';
import TopFollowers from './components/topfollowers';
import PostLanguage from './components/postlanguage'
import PostsDay from "./components/postsday";


export class View extends Component {
    state = {
        top_followers: [],
        postday: [],
        postlang: []
    };
    
    componentDidMount(){
        Promise.all([
            fetch('http://localhost:2222/get_info?id=1'),
            fetch('http://localhost:2222/get_info?id=2'),
            fetch('http://localhost:2222/get_info?id=3')
        ])
            .then(([res1, res2, res3]) => Promise.all([res1.json(), res2.json(), res3.json()]))
            .then(([data1, data2, data3]) => this.setState({
                top_followers: data1,
                postday: data2,
                postlang: data3
            }));
    }

    render() {
        if (this.props.tab === "1") {
            return (<TopFollowers followers_list={this.state.top_followers} />)
        } else if (this.props.tab === "2") {
            return (<PostsDay posts={this.state.postday} />)
        } else if (this.props.tab === "3") {
            return (<PostLanguage posts={this.state.postlang} />)
        }
    }
}

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {tab: "1"};
    }

    onOneClick = e => {
        this.setState({ tab: "1" });
    };
    onTwoClick = e => {
        this.setState({ tab: "2" });
    };
    onThreeClick = e => {
        this.setState({ tab: "3" });
    };

    render() {
        return (
            // <TopFollowers followers_list={this.state.response} />
            // <PostsDay posts={this.state.response} />
            // <PostLanguage posts={this.state.response} />
            <div>
                <button type="button" onClick={this.onOneClick}>Top Followers</button>
                <button type="button" onClick={this.onTwoClick}>Posts per Day</button>
                <button type="button" onClick={this.onThreeClick}>Posts per Language</button>
                <View tab={this.state.tab} />
            </div>
        )
    }
}
export default App;