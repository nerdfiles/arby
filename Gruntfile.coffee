path = require 'path'

module.exports = (grunt) ->
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-express-server'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-requirejs'
  grunt.loadNpmTasks 'grunt-contrib-htmlmin'
  grunt.loadNpmTasks 'grunt-contrib-copy'

  yoConfig =
      'app': 'app'
      'dist': 'dist'
      'build': 'build'

  grunt.initConfig

    pkg: grunt.file.readJSON 'package.json'

    yeoman: yoConfig

    requirejs:
      compile:
        options:
          name: 'app'
          baseUrl: './app'
          mainConfigFile: './app/boot_dist.js'
          out: './<%= yeoman.dist %>/<%= pkg.name %>.js'
          findNestedDependencies : true
          preserveLicenseComments: false
          optimizeAllPluginResources: true
          optimize: 'uglify2'
          logLevel: 0

    copy:
      main:
        files: [
          {
            expand: true
            flatten: true
            src: [
              './<%= yeoman.app %>/foundation/*.jade'
            ]
            dest: './<%= yeoman.build %>/foundation'
            filter: 'isFile'
          }
        ]

    express:
      dev:
        options:
          cmd: process.argv[0]
          background: true
          delay: 0
          script: './<%= yeoman.build %>/server.js'
          debug: false

    coffee:
      glob_to_multiple:
        expand: true
        flatten: true
        src: ['./<%= yeoman.app %>/*.coffee']
        dest: './<%= yeoman.build %>/'
        ext: '.js'
      compile_api:
        files:
          './<%= yeoman.app %>/routes/base.js': [
            './<%= yeoman.app %>/routes/*.coffee'
          ]
      compile_services:
        expand: true,
        flatten: true,
        src: [
          './<%= yeoman.app %>/services/*.coffee'
        ]
        dest: './<%= yeoman.build %>/services'
        ext: '.js'
      compile_modules:
        expand: true,
        flatten: false,
        src: [
          './<%= yeoman.app %>/modules/**/*.coffee'
        ]
        dest: './<%= yeoman.build %>/modules/..'
        ext: '.js'


    htmlmin:
        dist:
          options:
            removeComments: true
            collapseWhitespace: true
          files:
            './<%= yeoman.build %>/foundation/index.dist.html': './<%= yeoman.app %>/foundation/index.dist.html'
            './<%= yeoman.build %>/foundation/index.html': './<%= yeoman.app %>/foundation/index.html'

    watch:
      express:
        files:  [
          './<%= yeoman.app %>/models/*.coffee'
          './<%= yeoman.app %>/modules/**/*.coffee'
          './<%= yeoman.app %>/services/**/*.coffee'
          './<%= yeoman.app %>/*.coffee'
        ]
        tasks:  [
          'coffee',
          'express:dev'
        ]
        options:
          spawn: false

  # @name default
  # @memberof module:Gruntfile
  grunt.registerTask 'default', [
    'copy'
    'htmlmin'
    'coffee'
    'express:dev'
    'watch'
  ]

  # @name build
  # @memberof module:Gruntfile
  grunt.registerTask 'build', [
    'coffee'
    'requirejs:compile'
  ]
