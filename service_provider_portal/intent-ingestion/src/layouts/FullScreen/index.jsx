import React from 'react';

const Layout = ({className, children})=>{
  return (
    <>
      <main className={className}>
        {children}
      </main>
    </>
  );
};

export default Layout;
