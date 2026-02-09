package gui;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Modality;
import javafx.stage.Stage;
import fachlogik.Risiko1;

public class Extremesrisiko1 extends Stage {

    private Risiko1 risiko;

    public Extremesrisiko1(Stage parent, Risiko1 risiko) {
        this.risiko = risiko;
        initOwner(parent);
        initModality(Modality.WINDOW_MODAL);
    }

    public void zeige() {

        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);

        Label bez = new Label(risiko.getBezeichnung());
        Label mass = new Label(risiko.getMassnahme());
        TextField beitrag = new TextField();

        grid.addRow(0, new Label("Bezeichnung:"), bez);
        grid.addRow(1, new Label("Maßnahme:"), mass);
        grid.addRow(2, new Label("Versicherungsbeitrag:"), beitrag);

        Button ok = new Button("OK");
        ok.setOnAction(e -> {
            try {
                float wert = Float.parseFloat(beitrag.getText());
                risiko.setVersicherungsbeitrag(wert);
                close();
            } catch (NumberFormatException ex) {
                Alert alert = new Alert(Alert.AlertType.ERROR, "Ungültiger Wert für Versicherungsbeitrag!");
                alert.showAndWait();
            }
        });

        Button abbr = new Button("Abbrechen");
        abbr.setOnAction(e -> close());

        HBox hb = new HBox(10, ok, abbr);
        hb.setAlignment(Pos.CENTER);
        hb.setPadding(new Insets(10));

        BorderPane bp = new BorderPane();
        bp.setCenter(grid);
        bp.setBottom(hb);

        setScene(new Scene(bp, 340, 180));
        setTitle("Extremes Risiko");
        showAndWait();
    }
}
