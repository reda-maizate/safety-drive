import Header from '../Header';
import Footer from '../Footer';

type children = { 
    children : React.ReactNode;
}

export default function Layout({ children }: children){
    return (
      <>
        <Header />
        {children}
        <Footer />
      </>
    )
}