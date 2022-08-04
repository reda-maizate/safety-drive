import Image from 'next/image';

import FormLogin from '../FormLogin';

import loginImg from '../assets/loginimg.jpg';

export default function Login() {
  return (
    <div className="relative w-full h-screen bg-zinc-900/90">
      <div className="-z-10 h-screen absolute w-full object-cover mix-blend-overlay">
        <Image layout="fill" src={loginImg} alt="/" />
      </div>
      <FormLogin />
    </div>
  )
}