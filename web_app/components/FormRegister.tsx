import {FcGoogle} from 'react-icons/fc';
import {AiFillFacebook} from 'react-icons/ai';
import Link from 'next/link';

export default function FormLogin() {
    return (
      <div className="flex justify-center items-center h-full z-1">
        <form className="max-w-[400px] w-full mx-auto bg-white p-8">
          <h2 className="text-4xl font-bold text-center py-4">BRAND.</h2>
          <div className="flex justify-between py-8">
            <p className="border shadow-lg hover:shadow-xl px-6 py-2 relative flex items-center">
              <AiFillFacebook className="mr-2" /> Facebook
            </p>
            <p className="border shadow-lg hover:shadow-xl px-6 py-2 relative flex items-center">
              <FcGoogle className="mr-2" /> Google
            </p>
          </div>
          <div className="flex flex-col mb-4">
            <label>First Name</label>
            <input className="border relative bg-gray-100 p-2" type="text" />
          </div>
          <div className="flex flex-col mb-4">
            <label>Lastname</label>
            <input className="border relative bg-gray-100 p-2" type="text" />
          </div>
          <div className="flex flex-col mb-4">
            <label>Email</label>
            <input className="border relative bg-gray-100 p-2" type="email" />
          </div>
          <div className="flex flex-col mb-4">
            <label>Username</label>
            <input className="border relative bg-gray-100 p-2" type="text" />
          </div>
          <div className="flex flex-col ">
            <label>Password</label>
            <input
              className="border relative bg-gray-100 p-2"
              type="password"
            />
          </div>

          <button className="w-full py-3 mt-8 bg-indigo-600 hover:bg-indigo-500 relative text-white">
            Sign Up
          </button>
          <p className="flex items-center mt-2">
            <input className="mr-2" type="checkbox" />
            Remember Me
          </p>
          <p className="text-center mt-8">
            Already have an account ?{' '} <Link href="/" passHref>Log in</Link>
          </p>
        </form>
      </div>
    )
}