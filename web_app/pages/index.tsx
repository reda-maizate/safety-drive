import type { NextPage } from 'next';
import Head from 'next/head';
import Layout from '../components/layout/Layout';
import Login from '../components/layout/Login';

const Home: NextPage = () => {
  return (
    <Layout>
      <Head>
        <title>Login Page</title>
        <meta name="description" content="Safety drive login page" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Login />
    </Layout>
  )
}

export default Home
