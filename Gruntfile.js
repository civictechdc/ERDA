module.exports = function(grunt){
  grunt.initConfig({
    pkg : grunt.file.readJSON('package.json'),
    
    clean : {
      build : ['assets/js']
    },

    browserify : {
      dist : {
        files : {
          'assets/js/<%= pkg.name %>.js' : ['src/scripts/main.js'],
        }
      },
      debug : {
        files : {
          'assets/js/<%= pkg.name %>.js' : ['src/scripts/main.js'],
        },
        bundleOptions : {
          debug : true
        }
      }
    },
    uglify : {
      dist : {
        files : {
          'assets/js/<%= pkg.name %>.js' : ['assets/js/<%= pkg.name %>.js']
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  grunt.registerTask('debug', [
    'clean:build',
    'browserify:debug'
  ]);

  grunt.registerTask('dist', [
    'clean:build',
    'browserify:dist',
    'uglify:dist'
  ]);
};
