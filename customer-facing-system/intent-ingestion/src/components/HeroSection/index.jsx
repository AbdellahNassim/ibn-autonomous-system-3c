import React from 'react';
const HeroSection = ()=>{
  return (
    <div className="flex content-center
    items-center justify-center h-full bg-black-lighter">
      <div className="flex flex-col w-6/12 text-center">
        <h1 className="text-white text-7xl font-semibold">
            Your story starts with an intent.
        </h1>
        <p className="text-white  text-lg font-thin mt-6">
            SCORING is a next generation platform that
            allows you to experience services that are optimized
            according to your requirements
        </p>
      </div>
    </div>
  );
};

export default HeroSection;
