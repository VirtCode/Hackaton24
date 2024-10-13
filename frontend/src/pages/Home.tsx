import React, { Dispatch, SetStateAction, useEffect, useState } from "react";
import {
  IonContent,
  IonGrid,
  IonPage,
  IonRow,
  IonLabel,
  IonText,
  IonList,
  IonToast,
  IonItem,
} from "@ionic/react";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/scrollbar";
import { Scrollbar, Navigation, Pagination, A11y } from "swiper/modules";
import "./Home.css";
import { Group, Mensa, Session } from "../api/group";
import Header from "../components/Header";
import MensaCard from "../components/MensaCard";
import HostAction from "../components/HostAction";
import ScannerModal from "../components/ScannerModal";

interface HomeProps {
  mensas: Mensa[];
  groups: Group[];
  activeSessions: Session[];
  setActiveSessions: Dispatch<SetStateAction<any[]>>;
  isToastOpen: boolean;
  setIsToastOpen: Dispatch<SetStateAction<boolean>>;
}

const Home: React.FC<HomeProps> = ({
  mensas,
  groups,
  activeSessions,
  setActiveSessions,
  isToastOpen,
}) => {
  const [isScannerOpen, setIsScannerOpen] = useState(false);

  const renderSession = (session: Session, idx: number) => {
    let start = new Date(session.start);
    let end = new Date(session.end);

    let diff = end.getTime() - new Date().getTime();
    let hours = Math.floor(diff / (1000 * 60 * 60));
    let minutes = Math.floor((diff - hours * (1000 * 60 * 60)) / (1000 * 60));

    let text = minutes + "min"
    if (hours > 0) text = hours + "h " + text;

    return (
      <IonItem
        key={idx}
        routerLink={`/session/${session.id}`}
        color="success"
        className="pending-session"
      >
      <div className="session-div">
        <b>{session.group?.name}</b>
        <div>
         at {session.mensa.name} until {" "}
        {("0" + end.getHours()).slice(-2)}:{("0" + end.getMinutes()).slice(-2)}
            {" "} ({text} remaining)
            </div>
            </div>
      </IonItem>
    );
  };

  useEffect(() => {}, [activeSessions]);

  const renderMensaCard = (mensa: Mensa, idx: React.Key) => {
    return (
      <SwiperSlide key={idx} id="slide-container">
        <MensaCard mensa={mensa} />
      </SwiperSlide>
    );
  };

  return (
    <IonPage>
      <Header pageTitle="Title" main={true} />
      <IonContent fullscreen>
        <IonGrid className="home-grid">
          {activeSessions.length > 0 && (
            <IonList title="Currently having food" lines="none">
              <h2>Currently having food</h2>
              {activeSessions.map((session, idx) =>
                renderSession(session, idx)
              )}
            </IonList>
          )}
          <IonRow>
            <IonText>
              <h2>Already Hungry?</h2>
            </IonText>
          </IonRow>
          <IonRow class="ion-align-items-start">
            <Swiper
              modules={[Navigation, Pagination, Scrollbar, A11y]}
              direction={"horizontal"}
              slidesPerView={window.screen.width > 900 ? 3 : 1}
              draggable={false}
              scrollbar={{ draggable: false }}
            >
              {mensas.map((mensa, idx) => renderMensaCard(mensa, idx))}
            </Swiper>
          </IonRow>
        </IonGrid>
        <HostAction
          openScan={() => {
            setIsScannerOpen(true);
          }}
        />
        <ScannerModal
          setIsScannerOpen={setIsScannerOpen}
          isScannerOpen={isScannerOpen}
        />
        <IonToast
          isOpen={isToastOpen}
          duration={3000}
          message={"Created Session!"}
          position="bottom"
          positionAnchor="tabs"
        />
      </IonContent>
    </IonPage>
  );
};

export default Home;
