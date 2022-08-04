import Image from 'next/image';

import FormLogin from '../FormLogin';

import loginImg from '../assets/loginimg.jpg';

export default function Login() {
    
  return (
    <div className="relative w-full h-screen bg-zinc-900/90">
      <Image
        layout="fill"
        className="absolute w-full h-full object-cover mix-blend-overlay z-0"
        src={loginImg}
        alt="/"
      />
       <FormLogin /> 

    </div>
  )
}