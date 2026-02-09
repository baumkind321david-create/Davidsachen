package gui;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Modality;
import javafx.stage.Stage;
import fachlogik.Risiko1;

public class InakzeptablesRisiko1 extends Stage {

    private Risiko1 risiko;

    public InakzeptablesRisiko1(Stage parent, Risiko1 risiko) {
        this.risiko = risiko;
        initOwner(parent);
        initModality(Modality.WINDOW_MODAL);
    }

    public void zeiged() {

        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);

        Label bez = new Label(risiko.getBezeichnung());
        TextField mass = new TextField(risiko.getMassnahme());

        grid.addRow(0, new Label("Bezeichnung:"), bez);
        grid.addRow(1, new Label("Maßnahme:"), mass);

        Button ok = new Button("OK");
        ok.setOnAction(e -> {
            risiko.setMassnahme(mass.getText());
            close();
        });

        Button abbr = new Button("Abbrechen");
        abbr.setOnAction(e -> close());

        HBox hb = new HBox(10, ok, abbr);
        hb.setAlignment(Pos.CENTER);
        hb.setPadding(new Insets(10));

        BorderPane bp = new BorderPane();
        bp.setCenter(grid);
        bp.setBottom(hb);

        setScene(new Scene(bp, 320, 160));
        setTitle("Inakzeptables Risiko");
        showAndWait();
    }
}
