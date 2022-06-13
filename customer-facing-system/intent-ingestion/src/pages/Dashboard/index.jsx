import React, {useEffect} from 'react';
import Layout from '../../layouts/SideBarLayout';
import {useLocation} from 'react-router-dom';
import WebChat from '../../components/WebChat';
import IntentTable from '../../components/IntentTable';

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
      <div className="grid grid-cols-12 gap-6">
        <IntentTable/>
        <WebChat/>
      </div>
    </Layout>);
}
