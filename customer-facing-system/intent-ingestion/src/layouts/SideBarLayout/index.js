import React, {useState} from 'react';
import Sidebar from '../../components/SideBar';
import Header from '../../components/DashboardHeader';

const Layout = ({className, children})=>{
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className={`${className} flex`}>

      {/* Sidebar */}
      <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      {/* Main Content Area */}
      <div>

        {/** Main Area Header */}
        <Header></Header>

        {/** Main content  */}
        <main>
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
