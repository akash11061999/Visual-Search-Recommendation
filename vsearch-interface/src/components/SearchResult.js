import React, { Component } from 'react';
import Navbar from './NavBar';
import Loading from './Loading';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import { Container, Grid } from '@material-ui/core/';
import { CardActionArea, CardMedia } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
export default class SearchResult extends Component {

    constructor(props) {
        super(props);
        //this.state = this.props.location.state;
        this.state = {
            //isQueryImageUploaded: true,
            isQueryImageUploaded: this.props.location.state.isQueryImageUploaded,
            queryImg: this.props.location.state.queryImg,
            result: []
        }
        //console.log(this.state);
    }

    componentDidMount() {
        let url = "http://localhost:5000/predict";
        const data = new FormData();
        data.append('file', this.state.queryImg);
        console.log(data);

        let rawData;

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
                    result: res
                })
            }).catch((error) => {
                console.log(error);
            })

    }

    render() {
        if (this.state.isQueryImageUploaded) {
            return (
                <React.Fragment style={{
                    backgroundColor: '#f7f9fc',
                }}>
                    <Container
                        maxWidth="lg"
                        style={{
                            position: "relative",
                            marginTop: "75px",
                            //backgroundColor: '#ECF0F1'
                        }}>
                        <Navbar />
                        <Grid container spacing={3}>
                            {
                                this.state.result.map((data) => {
                                    return (
                                        <Grid item xs={4}>
                                            <Card style={{ maxWidth: 345 }}>
                                                <CardActionArea>
                                                    <CardMedia
                                                        component="img"
                                                        height="200px"
                                                        src={`data:image/jpeg;base64,${data[2]}`}
                                                        title="Contemplative Reptile"
                                                    />
                                                    <CardContent>
                                                        <Typography gutterBottom variant="h5" component="h2">
                                                            {data[1]}
                                                        </Typography>
                                                        <Typography variant="body2" color="textSecondary" component="p">
                                                            INR {data[3]}
                                                        </Typography>
                                                    </CardContent>
                                                </CardActionArea>
                                            </Card>
                                        </Grid>

                                    )
                                })
                            }
                        </Grid>
                    </Container>
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