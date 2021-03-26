import React, { Component } from 'react';
import Navbar from './NavBar';
import Loading from './Loading';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import {CardActionArea, CardMedia} from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
export default class SearchResult extends Component {

    constructor(props) {
        super(props);
        //this.state = this.props.location.state;
        this.state = {
            isQueryImageUploaded: this.props.location.state.isQueryImageUploaded,
            queryImg: this.props.location.state.queryImg,
            res: []
        }
        console.log(this.state);
    }

    componentDidMount() {
        let url = "http://localhost:5000/predict";
        const data = new FormData();
        data.append('file', this.state.queryImg);
        console.log(data);
        fetch(url, {
            method: 'post',
            body: data,
        })
            .then((response) => response.json())
            .then((res) => {
                console.log(res);
                this.setState({
                    isQueryImageUploaded: true,
                    queryImg: this.props.location.state.queryImg,
                    res: res
                })
            }).catch((error) => {
                console.log(error);
            })
    }
    render() {
        if (this.state.isQueryImageUploaded) {
            return (
                <React.Fragment>
                    <Navbar />
                    {
                        this.state.res.map((item) => {
                            return (
                                <Card style={{maxWidth: 345}}>
                                    <CardActionArea>
                                        <CardMedia
                                            component="img"
                                            height="200px"
                                            image={require("../assets/1.jpg")}
                                            //image="https://drive.google.com/uc?export=download&id=17jdlTZEqcC-LUY9Et_wimNQD0Q8LoIQO"
                                            title="Contemplative Reptile"
                                        />
                                        <CardContent>
                                            <Typography gutterBottom variant="h5" component="h2">
                                                ZARA Exclusive Top
                                            </Typography>
                                            <Typography variant="body2" color="textSecondary" component="p">
                                                INR 99
                                            </Typography>
                                        </CardContent>
                                    </CardActionArea>
                                </Card>

                            )
                        })
                    }
                </React.Fragment>
            )
        }
        else {
            return (
                <React.Fragment>
                    <Loading />
                </React.Fragment>
            )
        }
    }
}