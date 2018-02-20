Welcome to LogoDetect! This repository contains the frontend code for the application.

This project was bootstrapped with Create React App.

Below you will find some information on how to perform common tasks.
You can find the most recent version of this guide here.

For the project to build:

public/index.html is the page template;
src/index.js is the JavaScript entry point.
Available Scripts

In the project directory, you can run:

npm start

Runs the app in the development mode. Open http://localhost:3000 to view it in the browser.

The page will reload if you make edits. You will also see any lint errors in the console.

npm test

Launches the test runner in the interactive watch mode. See the section about running tests for more information.

npm run build

Builds the app for production to the build folder. It correctly bundles React in production mode and optimizes the build for the best performance.

npm run eject

Note: this is a one-way operation. Once you eject, you can’t go back!

If you aren’t satisfied with the build tool and configuration choices, you can eject at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except eject will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use eject. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

Displaying Lint Output in the Editor

Some editors, including Sublime Text, Atom, and Visual Studio Code, provide plugins for ESLint.

They are not required for linting. You should see the linter output right in your terminal as well as the browser console. However, if you prefer the lint results to appear right in your editor, there are some extra steps you can do.

You would need to install an ESLint plugin for your editor first. Then, add a file called .eslintrc to the project root:

{
  "extends": "react-app"
}
Now your editor should report the linting warnings.

Note that even if you edit your .eslintrc file further, these changes will only affect the editor integration. They won’t affect the terminal and in-browser lint output. This is because Create React App intentionally provides a minimal set of rules that find common mistakes.

If you want to enforce a coding style for your project, consider using Prettier instead of ESLint style rules.

Visual Studio Code

You would need to have the latest version of VS Code and VS Code Chrome Debugger Extension installed.

Then add the block below to your launch.json file and put it inside the .vscode folder in your app’s root directory.

{
  "version": "0.2.0",
  "configurations": [{
    "name": "Chrome",
    "type": "chrome",
    "request": "launch",
    "url": "http://localhost:3000",
    "webRoot": "${workspaceRoot}/src",
    "sourceMapPathOverrides": {
      "webpack:///src/*": "${webRoot}/*"
    }
  }]
}
Start your app by running npm start, and start debugging in VS Code by pressing F5 or by clicking the green debug icon. You can now write code, set breakpoints, make changes to the code, and debug your newly modified code—all from your editor.

WebStorm

You would need to have WebStorm and JetBrains IDE Support Chrome extension installed.

In the WebStorm menu Run select Edit Configurations.... Then click + and select JavaScript Debug. Paste http://localhost:3000 into the URL field and save the configuration.

Start your app by running npm start, then press ^D on macOS or F9 on Windows and Linux or click the green debug icon to start debugging in WebStorm.

The same way you can debug your application in IntelliJ IDEA Ultimate, PhpStorm, PyCharm Pro, and RubyMine.

Formatting Code Automatically

Prettier is an opinionated code formatter with support for JavaScript, CSS and JSON. With Prettier you can format the code you write automatically to ensure a code style within your project. See the Prettier's GitHub page for more information, and look at this page to see it in action.

To format our code whenever we make a commit in git, we need to install the following dependencies:

npm install --save husky lint-staged prettier
Alternatively you may use yarn:

yarn add husky lint-staged prettier
husky makes it easy to use githooks as if they are npm scripts.
lint-staged allows us to run scripts on staged files in git. See this blog post about lint-staged to learn more about it.
prettier is the JavaScript formatter we will run before commits.
Now we can make sure every file is formatted correctly by adding a few lines to the package.json in the project root.

Add the following line to scripts section:

  "scripts": {
+   "precommit": "lint-staged",
    "start": "react-scripts start",
    "build": "react-scripts build",
Next we add a 'lint-staged' field to the package.json, for example:

  "dependencies": {
    // ...
  },
+ "lint-staged": {
+   "src/**/*.{js,jsx,json,css}": [
+     "prettier --single-quote --write",
+     "git add"
+   ]
+ },
  "scripts": {
Now, whenever you make a commit, Prettier will format the changed files automatically. You can also run ./node_modules/.bin/prettier --single-quote --write "src/**/*.{js,jsx,json,css}" to format your entire project for the first time.

Next you might want to integrate Prettier in your favorite editor. Read the section on Editor Integration on the Prettier GitHub page.
