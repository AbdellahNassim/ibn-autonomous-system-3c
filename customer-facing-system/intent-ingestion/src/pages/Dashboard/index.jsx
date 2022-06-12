import React, {useEffect} from 'react';
import Layout from '../../layouts/SideBarLayout';
import {useLocation} from 'react-router-dom';

/**
 * Dashboard Home component
 * @return {*}
 */
export default function Dashboard() {
  const location = useLocation();

  /**
   * allows to scroll back to the start of the page each time
   * user change page
   */
  useEffect(() => {
    document.querySelector('html').style.scrollBehavior = 'auto';
    window.scroll({top: 0});
    document.querySelector('html').style.scrollBehavior = '';
  }, [location.pathname]); // triggered on route change


  return (
    <Layout className="h-screen overflow-hidden">
      <div>
         Heyyy
      </div>
    </Layout>);
}
