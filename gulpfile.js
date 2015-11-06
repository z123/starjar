var gulp = require('gulp');
var sass = require('gulp-sass');

var config = {
    bootstrapDir: './node_modules/bootstrap-sass',
    bootswatchDir: './node_modules/bootswatch',
    publicDir: './public'
};

gulp.task('css', function() {
    return gulp.src('./app/static/css/app.scss')
    .pipe(sass({
        includePaths: [config.bootstrapDir + '/assets/stylesheets',
                       config.bootswatchDir],
    }))
    .pipe(gulp.dest(config.publicDir + '/css'));
});

gulp.task('fonts', function() {
    return gulp.src(config.bootstrapDir + '/assets/fonts/**/*')
    .pipe(gulp.dest(config.publicDir + '/fonts'));
});

gulp.task('js', function() {
    // TODO: Put bootstrap js in here to?
    return gulp.src(['./app/static/js/app.js'])
});

gulp.task('default', ['css', 'fonts', 'js']);
