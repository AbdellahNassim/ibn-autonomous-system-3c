import React from 'react';
import {Disclosure} from '@headlessui/react';
import {MenuIcon, XIcon} from '@heroicons/react/outline';
import Navigations from './navigation-data.json';
import ScoringLogo from '../../assets/scoring_logo.png';
import {useAuth} from '../../utils/auth';

const NavBar = ()=>{
  const auth = useAuth();


  return (
    <Disclosure as="nav" className="z-10 w-full bg-black-lighter ">
      {({open}) => (
        <>
          <div className=" px-6 sm:px-12 lg:px-12">
            <div className="relative w-full flex flex-row justify-center
            sm:justify-between h-14  sm:h-20 sm:pt-4">
              <div className="w-16 lg:block hidden">
                <img src={ScoringLogo} href="/" alt="SCORING" />
              </div>
              <div className="absolute inset-y-0
              left-0 flex items-center sm:hidden">
                {/* Mobile menu button */}
                <Disclosure.Button className="inline-flex items-center
                justify-center p-2 rounded-md text-gray-400 hover:text-white
                 hover:bg-gray-700 focus:outline-none focus:ring-2
                 focus:ring-inset focus:ring-white">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XIcon
                      className="block h-6 w-6 text-white-lighter"
                      aria-hidden="true"
                    />
                    ) : (
                    <MenuIcon
                      className="block h-6 w-6 text-white-lighter"
                      aria-hidden="true"
                    />
                          )}
                </Disclosure.Button>
              </div>
              <div className="sm:hidden block">
                <h1 className=" text-white pt-3 text-xl">
                                SCORING System
                </h1>
              </div>
              <div className="hidden sm:flex flex-row items-center space-x-5
               md:space-x-8  mx-2">
                {Navigations.map((item, index) => (
                  <a
                    id={`${index}`}
                    href={item.href}
                    key={index}
                    className="text-white-lighter text-lg
                     md:text-lg lg:text-xl hover:text-black-default"
                  >
                    {item.title}
                  </a>
                ))}
              </div>
              <div className="hidden sm:flex flex-row text-center items-center">
                {
                  // check if we have a connected user
                  auth.getCurrentUser() ?
                  <a className=" bg-primary-500 cursor-pointer hover:bg-primary-800 text-white-default text-lg font-bold py-1 px-4 rounded-md"
                    href="/dashboard">
                    Dashboard
                  </a>:
                  <a className=" bg-primary-500 cursor-pointer hover:bg-primary-800 text-white-default text-lg font-bold py-1 px-4 rounded-md"
                    href="/login">
                    Login
                  </a>

                }

              </div>
            </div>
          </div>
          <Disclosure.Panel className="sm:hidden">
            <div className=" flex flex-col items-center  px-2 pb-3 space-y-1">
              {Navigations.map((item) => (
                <a
                  key={item.title}
                  href={item.href}
                  className={` block hover:text-black-default px-3 pb-2 
                  rounded-md text-base font-medium text-center 
                  text-white-lighter `}
                  aria-current={item.current ? 'page' : undefined}
                >
                  {item.title}
                </a>
              ))}
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
};

export default NavBar;
