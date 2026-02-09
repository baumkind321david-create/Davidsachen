package gui;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Modality;
import javafx.stage.Stage;
import fachlogik.Risiko1;

public class Risikoerfassung1 extends Stage {

    private Risiko1 risiko;

    public Risikoerfassung1(Stage parent, Risiko1 risiko) {
        this.risiko = risiko;
        initOwner(parent);
        initModality(Modality.WINDOW_MODAL);
    }

    public Risiko1 zeigeFenster() {

        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);

        TextField bez = new TextField(risiko.getBezeichnung());
        TextField wkeit = new TextField(Float.toString(risiko.getEintrittswahrscheinlichkeit()));
        TextField kosten = new TextField(Float.toString(risiko.getKostenImSchadensfall()));

        grid.addRow(0, new Label("Bezeichnung:"), bez);
        grid.addRow(1, new Label("Eintrittswahrscheinlichkeit:"), wkeit);
        grid.addRow(2, new Label("Kosten im Schadensfall:"), kosten);

        Button ok = new Button("OK");
        ok.setOnAction(e -> {
            try {
                risiko.setBezeichnung(bez.getText());
                risiko.setEintrittswahrscheinlichkeit(Float.parseFloat(wkeit.getText()));
                risiko.setKostenImSchadensfall(Float.parseFloat(kosten.getText()));
                close();
            } catch (NumberFormatException ex) {
                Alert alert = new Alert(Alert.AlertType.ERROR, "Ungültige Zahlenangaben!");
                alert.showAndWait();
            }
        });

        Button abbr = new Button("Abbrechen");
        abbr.setOnAction(e -> {
            risiko = null;
            close();
        });

        HBox hb = new HBox(10, ok, abbr);
        hb.setAlignment(Pos.CENTER);
        hb.setPadding(new Insets(10));

        BorderPane bp = new BorderPane();
        bp.setCenter(grid);
        bp.setBottom(hb);

        setScene(new Scene(bp, 320, 180));
        setTitle("Risiko erfassen");
        showAndWait();

        return risiko;
    }
}
