package gui;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;

import datenhaltung.PersistenzException;
import datenhaltung.RisikoDerialiserung;
import fachlogik.*;

public class Risikoverwaltung1 extends Application {

    private Risikoverwaltung risikoverwaltung;
    private ObservableList<Risiko1> observableRisiken;
    private ListView<Risiko1> risikoListView;

    private final String pfad = "C:\\Users\\baumk\\OneDrive\\Desktop\\Uni\\versuch1\\";

    public static void main(String[] args) {
        launch(args);
    }

    public Risikoverwaltung1() {
        risikoverwaltung = new Risikoverwaltung();
    }

    @Override
    public void start(Stage primaryStage) {

        BorderPane root = new BorderPane();

        observableRisiken = FXCollections.observableArrayList();
        observableRisiken.setAll(risikoverwaltung.getRisikenListe());

        risikoListView = new ListView<>(observableRisiken);
        root.setCenter(risikoListView);

        MenuBar menuBar = new MenuBar();

        /* ---------------- Datei ---------------- */
        Menu datei = new Menu("Datei");

        MenuItem laden = new MenuItem("Laden");
        laden.setOnAction(e -> {
            try {
                String dateiname = InputView
                        .create(primaryStage, "Laden", "Dateiname:", null)
                        .showView();
                if (dateiname == null) return;

                RisikoDerialiserung rd = new RisikoDerialiserung(pfad + dateiname);
                risikoverwaltung.setRisikoDerialiserung(rd);
                risikoverwaltung.laden();

                observableRisiken.setAll(risikoverwaltung.getRisikenListe());
            } catch (PersistenzException ex) {
                ex.printStackTrace();
            }
        });

        MenuItem speichern = new MenuItem("Speichern");
        speichern.setOnAction(e -> {
            try {
                String dateiname = InputView
                        .create(primaryStage, "Speichern", "Dateiname:", null)
                        .showView();
                if (dateiname == null) return;

                RisikoDerialiserung rd = new RisikoDerialiserung(pfad + dateiname);
                risikoverwaltung.setRisikoDerialiserung(rd);
                risikoverwaltung.speichernin();
            } catch (PersistenzException ex) {
                ex.printStackTrace();
            }
        });

        MenuItem export = new MenuItem("Risikoliste in Datei");
        export.setOnAction(e -> {
            String dateiname = InputView
                    .create(primaryStage, "Export", "Dateiname:", "risiken.txt")
                    .showView();
            if (dateiname == null) return;

            try (BufferedWriter bw = new BufferedWriter(new FileWriter(pfad + dateiname))) {
                for (Risiko1 r : risikoverwaltung) {
                    bw.write(r.toString());
                    bw.newLine();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        });

        MenuItem beenden = new MenuItem("Beenden");
        beenden.setOnAction(e -> primaryStage.close());

        datei.getItems().addAll(laden, new SeparatorMenuItem(),
                speichern, new SeparatorMenuItem(),
                export, new SeparatorMenuItem(),
                beenden);

        /* ---------------- Risiko ---------------- */
        Menu risiko = new Menu("Risiko");

        MenuItem neu = new MenuItem("Neues Risiko");
        neu.setOnAction(e -> {

            Risiko1 basis = new AkzeptablesRisiko();
            Risikoerfassung1 erfassung = new Risikoerfassung1(primaryStage, basis);
            Risiko1 tmp = erfassung.zeigeFenster();
            if (tmp == null) return;

            float wert = tmp.berechneRisikowert();
            float kosten = tmp.getKostenImSchadensfall(); // korrekte Methode

            Risiko1 finalRisiko;

            if (wert < 500_000) {
                finalRisiko = tmp;
            } else if (kosten > 1_000_000) {
                finalRisiko = new extrem(tmp);
                new Extremesrisiko1(primaryStage, finalRisiko).zeige();
            } else {
                finalRisiko = new inakze(tmp);
                new InakzeptablesRisiko1(primaryStage, finalRisiko).zeiged();
            }

            risikoverwaltung.aufnehmen(finalRisiko);
            observableRisiken.add(finalRisiko);
        });

        risiko.getItems().add(neu);

        /* ---------------- Anzeige ---------------- */
        Menu anzeige = new Menu("Anzeige");

        MenuItem maxRueck = new MenuItem("Maximale Rückstellung");
        maxRueck.setOnAction(e -> {
            Risiko1 max = risikoverwaltung.sucheRisikoMitMaxRueckstellung();
            if (max != null) {
                MessageView.create(primaryStage, "Maximale Rückstellung", max.toString()).showView();
            }
        });

        MenuItem summe = new MenuItem("Summe Rückstellungen");
        summe.setOnAction(e -> {
            MessageView.create(primaryStage, "Summe Rückstellungen",
                  
                    String.valueOf(risikoverwaltung.neuberechneSummeRueckstellungen())
            ).showView();
        });


        anzeige.getItems().addAll(maxRueck, new SeparatorMenuItem(), summe);

        menuBar.getMenus().addAll(datei, risiko, anzeige);
        root.setTop(menuBar);

        primaryStage.setScene(new Scene(root, 600, 400));
        primaryStage.setTitle("Risikoverwaltung");
        primaryStage.show();
    }
}
