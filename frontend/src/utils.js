const utils = {
    URL: 'https://image.tmdb.org/t/p/',
    SIZES: {
        W185: 'w185',
        W780: 'w780',
        W1280: 'w1280',
    },
    UNAVAILABLE: require('./assets/default_w185.jpg'),
    poster(result) {
        if (result.media_type === "person")
            return result.profile_path ? (this.URL + this.SIZES.W185 + result.profile_path) : this.UNAVAILABLE;
        return result.poster_path ? (this.URL + this.SIZES.W185 + result.poster_path) : this.UNAVAILABLE;
    },
    season_poster(result) {
        return result.poster_path ? (this.URL + this.SIZES.W185 + result.poster_path) : this.UNAVAILABLE;
    },
    title(result) {
        if (result.media_type == "movie")
            return result.title;
        return result.name;
    },
    original_title(result) {
        if (result.media_type == "movie")
            return result.original_title;
        else if (result.media_type == "tv")
            return result.original_name;
        return result.name;
    },
    backdrop(result) {
        return this.URL + this.SIZES.W1280 + result.backdrop_path;
    },
}

export default utils;
