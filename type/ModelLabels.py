from typing import List, Dict
import math

class ModelLabels:
    def __init__(self, records: List[Dict]):
        # -- Separation of the products and the catalogs
        products = []
        lbls = []

        lbl_cls = 29;  # This class belongs to the yaml of training and its for labels
        empty_cls = 28;
        empties = 0;

        for idx, record in enumerate(records):
            record['idx'] = idx
            if record['class'] == lbl_cls:
                lbls.append(record)
            else:
                products.append(record)
            if record['class'] == empty_cls:
                empties += 1

        self.empties = empties
        self.labeled, self.unlabeled = self.get_labeled_unlabeled(products, lbls)
        self.products = self.get_products(products)

    # Gets the center from the rectangles of the inference
    def get_centers(self, xmin, xmax, ymin, ymax):
        return (xmin + xmax) / 2, (ymin + ymax) / 2

    # From the records creates a new list with the y and x center of the rectangle
    def parse_centers(self, records):
        centers = []
        for r in records:
            xc, yc = self.get_centers(r['xmin'], r['xmax'], r['ymin'], r['ymax'])
            centers.append({"xc": xc, "yc": yc, 'class': r['class'], 'name': r['name'], "idx": r['idx']})
        return centers

    # euclidian distance
    def dist(self, p1, pd):
        x = (p1[0] - pd[0]) ** 2
        y = (p1[1] - pd[1]) ** 2
        return math.sqrt(x + y)

    def getEmpties(self):
        return self.empties

    # return labeled, unlabeled as list of products with their id
    def get_labeled_unlabeled(self, products, lbls):
        pcenters = self.parse_centers(products)
        lcenters = self.parse_centers(lbls)

        labeled = []
        while len(lcenters) > 0:
            lc = lcenters.pop(0);  # Get the first label
            distances = []

            for pc in pcenters:
                lbl_p = [lc['xc'], lc['yc']]  # Label x,y point
                product_p = [pc['xc'], pc['yc']]  # Product x,y point
                distance = self.dist(lbl_p, product_p)  # Getting the distance from the label and the products
                distances.append(distance)

            m_idx = distances.index(min(distances))  # Get index of the product closer to the label
            p_val = pcenters.pop(m_idx)  # Pop that product
            labeled.append(p_val['idx'])  # Save the labeled product
        unlabeled = [p['idx'] for p in pcenters]

        return labeled, unlabeled

    def get_products(self, products):
        temp_p = []
        for p in products:
            if p['idx'] in self.labeled:
                p['labeled'] = 1
                temp_p.append(p)
            else:
                p['labeled'] = 0
                temp_p.append(p)

        return temp_p