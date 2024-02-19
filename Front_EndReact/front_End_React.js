import React from 'react';

// Creating a component without JSX
function HelloWorld() {
  // Using React.createElement to create a simple element
  return React.createElement('div', null,
    React.createElement('h1', null, 'Hello, World!')
  );
}


export default HelloWorld;