import React from 'react';
import NavBar from '../../components/NavBar';

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
