import React, { Component } from 'react';
import Navbar from './NavBar'
import ItemCard from './ItemCard'
import { Container, Card, CardActionArea, CardMedia, CardContent, Typography } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import SearchResult from './SearchResult';
import { TextRotateUp } from '@material-ui/icons';
import Loading from './Loading';


export default class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isQueryImageUploaded: false,
            queryImg: {},
            isLoading: true,
            homeData: []
        }
    }

    componentDidMount() {
        console.log("Home!");
        let url = "http://localhost:5000/home/data";
        let rawData;

        fetch(url, {
            method: 'get'
        })
            .then((response) => response.json())
            .then((res) => {
                //console.log(res);
                this.setState({
                    isQueryImageUploaded: false,
                    queryImg: {},
                    isLoading: false,
                    homeData: res,
                })
            }).catch((error) => {
                console.log(error);
            })
        console.log(this.state.homeData);
    }

    render() {
        if (this.state.isLoading) {
            return (
                <React.Fragment>
                    <Loading />
                </React.Fragment>
            )
        }
        else {
            if (this.state.isQueryImageUploaded) {
                return (
                    <React.Fragment>
                        <SearchResult />
                    </React.Fragment>
                )
            }
            else {
                return (
                    <React.Fragment style={{
                        backgroundColor: '#f7f9fc',
                    }}>
                        <Container
                            maxWidth="lg"
                            style={{
                                position: "relative",
                                marginTop: "75px",
                                //backgroundColor: '#f7f9fc',
                                padding: "2%"
                            }}>
                            <Navbar props={this.props} />
                            <Grid container spacing={3}>
                                {
                                    this.state.homeData.map((data) => {
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
        }
    }
}