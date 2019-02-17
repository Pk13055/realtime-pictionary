# Flask Blueprint App

## Introduction

This is a blueprint for multimodule flask apps. The basic skeleton has been setup, all you have to do is follow the comments to plug in your own modules. It uses `sqlite3` as the database.

## How to use

- `git clone https://github.com/Pk13055/flask-app-blueprint.git `
- `cd flask-app-blueprint`
- `pipenv install`
- `rm -rf .git ` (_optional_)

## Environment Variables

- Set `$ENV` to either production or dev
- Set/unset `$DEBUG` to toggle logging
- Set `$DATABASE_URL` to access the `DATABASE_URI` from the code

## Specifications

- Basic routing and a home module have been added.
- No models are added so that can be customized according to your needs.
- Ships with bootstrap CDN and jQuery for rapid development.
- `base.html` routing with template inheritance also already in place. 
- CSRF protection right out of the box.
- CAS support as well.
- Ships with a config file to handle global app settings. 
- Some what _MVC architecture_
