import React from 'react';
import NavBar from '../NavBar';

const Layout = ({className, children})=>{
  return (
    <>
      <NavBar/>
      <main className={className}>
        {children}
      </main>
    </>
  );
};

export default Layout;
