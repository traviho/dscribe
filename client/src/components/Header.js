import React, { Component } from 'react';

class Header extends Component {
  state = {
    data: null
  };

  render() {
    return (
      <nav className="menu transparent z-depth-2"
           data-target="top"
           id="topbar"
           ref={(e) => {
             if (e) {
               e.style.setProperty('background-color', '#212121', 'important');
             }
           }}>
        <div className="nav-wrapper">
          <a href="/" className="brand-logo title left offset-left">dscribe</a>
        </div>
      </nav>
    );
  }
}

export default Header;
